alert("hello");
odoo.define(['jszip', 'ods'], function (jszip, ods) {
    "use strict";
        var zip = new JSZip();
        var count = 0;
        var zipFilename = "zipFilename.zip";
        
           $(document).ready( function () {
$('#table_id').DataTable();
} );
            
