// odoo.define('technical_service_request.request_form', function (require) {
//     'use strict';
  
//     const publicWidget = require('web.public.widget');
  
//     publicWidget.registry.RequestForm = publicWidget.Widget.extend({
//         selector: '#service-request-form',
//         start: function () {
//           this._loadEquipments();
//           return this._super.apply(this, arguments);
//         },
//         _loadEquipments: function () {
//           const $select = this.$el.find('#equipment-select');
//           $select.empty().append($('<option>', { value: '', text: 'Loading...' }));
//           this._rpc({
//             route: '/request-service/equipments',
//             params: {},
//           }).then(function (result) {
//             $select.empty();
//             result.forEach(equipment => {
//               $select.append($('<option>', { value: equipment, text: equipment }));
//             });
//           });
//         },
//       });
  
//     return publicWidget.registry.RequestForm;
//   });
  