frappe.ui.form.on('Umrah Booking', {
    refresh: function(frm) {
        // Show Create Sales Invoice button if booking is saved, has pilgrims, and no invoice exists yet
        if (!frm.is_new() && !frm.doc.sales_invoice && frm.doc.total_pilgrims > 0) {
            frm.add_custom_button(__('Create Sales Invoice'), function() {
                frappe.confirm(
                    __('Are you sure you want to create and submit a Sales Invoice for this booking?'),
                    function() {
                        frappe.call({
                            method: 'business_management.business_management.doctype.umrah_booking.umrah_booking.create_sales_invoice',
                            args: {
                                booking_name: frm.doc.name
                            },
                            freeze: true,
                            freeze_message: __('Generating Invoice...'),
                            callback: function(r) {
                                if (r.message) {
                                    frappe.show_alert({
                                        message: __('Sales Invoice {0} created and submitted successfully', [r.message]),
                                        indicator: 'green'
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __('Actions'));
        }
    },

    package: function(frm) {
        frm.trigger('fetch_rate');
    },

    sharing_type: function(frm) {
        frm.trigger('fetch_rate');
    },

    fetch_rate: function(frm) {
        if (frm.doc.package && frm.doc.sharing_type) {
            const field_map = {
                'Sharing': 'price_sharing',
                'Quad': 'price_quad',
                'Triple': 'price_triple',
                'Double': 'price_double',
                'Single': 'price_single'
            };
            const rate_field = field_map[frm.doc.sharing_type];
            frappe.db.get_value('Umrah Package', frm.doc.package, rate_field, (r) => {
                if (r && r[rate_field] !== undefined) {
                    frm.set_value('rate', r[rate_field]);
                    frm.set_value('total_amount', (frm.doc.total_pilgrims || 0) * r[rate_field]);
                }
            });
        }
    }
});

// Auto-populate pilgrim details in child table when selecting a pilgrim
frappe.ui.form.on('Umrah Booking Pilgrim', {
    pilgrim: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.pilgrim) {
            frappe.db.get_value('Umrah Pilgrim', row.pilgrim, ['first_name', 'last_name', 'passport_number', 'visa_status'], (r) => {
                if (r) {
                    frappe.model.set_value(cdt, cdn, 'first_name', r.first_name);
                    frappe.model.set_value(cdt, cdn, 'last_name', r.last_name);
                    frappe.model.set_value(cdt, cdn, 'passport_number', r.passport_number);
                    frappe.model.set_value(cdt, cdn, 'visa_status', r.visa_status);
                }
            });
        }
    },
    pilgrims_add: function(frm) {
        // Trigger recount on client side when row is added
        frm.set_value('total_pilgrims', (frm.doc.pilgrims || []).length);
        if (frm.doc.rate) {
            frm.set_value('total_amount', frm.doc.total_pilgrims * frm.doc.rate);
        }
    },
    pilgrims_remove: function(frm) {
        // Trigger recount on client side when row is removed
        frm.set_value('total_pilgrims', (frm.doc.pilgrims || []).length);
        if (frm.doc.rate) {
            frm.set_value('total_amount', frm.doc.total_pilgrims * frm.doc.rate);
        }
    }
});
