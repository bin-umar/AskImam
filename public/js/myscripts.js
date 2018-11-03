var hijri = document.getElementById("hijri");
var grigorian = document.getElementById("grigorian");

hijri.innerHTML = HijriJS.todayHijri();
grigorian.innerHTML = HijriJS.todayGregorian();

tinymce.init({
  selector: 'textarea#tinymce',
  height: 120,
  menubar: false,
  plugins: [
    'advlist autolink lists link image charmap print preview anchor textcolor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code help wordcount'
  ],
  toolbar: 'insert | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
  content_css: [
    '/static/js/tinymce/skins/lightgray/codepen.min.css']
});