<div style="width:30mm; height:20mm; border:1px solid #ccc; font-family: Arial, sans-serif; box-sizing:border-box; padding:1mm;">
  <table style="width:100%; height:100%; border-collapse:collapse; font-size:8px;">
    <!-- Название -->
    <tr>
      <td colspan="2" style="font-weight:bold; font-size:9px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
        {{name}}
      </td>
    </tr>
    <!-- Артикул и цена -->
    <tr>
      <td style="font-size:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
        {{#isarticle}}{{article}}{{/isarticle}}
      </td>
      <td style="font-size:8px; text-align:right;">
        {{#isprice}}<b>{{price}}</b>{{/isprice}}
      </td>
    </tr>
    <!-- Штрихкод -->
    {{#isbarcode}}
    <tr>
      <td colspan="2" style="text-align:center; padding-top:1mm;">
        <img style="width:28mm; height:6mm;" {{{barcodeattr}}} />
        <div style="font-size:6px; line-height:1;">{{barcode}}</div>
      </td>
    </tr>
    {{/isbarcode}}
  </table>
</div>