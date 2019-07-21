
var f = [
  'invittes',
  'starttime',
  'closetime',
  'budgets',
  'deliverytime',
  'customization',
]

function autofill(e) {
  e.preventDefault();
  f['invittes'].input.value = '100';
  f['starttime'].input.value = '2019-01-01 00:00:01';
  f['closetime'].input.value = '2019-01-01 10:00:01';
  f['budgets'].input.value = 1000.00;
  f['deliverytime'].input.value = '08:00:00';
  f['customization'].input.value = 'None';
}
