var counter = 0;
const docCount = document.getElementById('docCount');

const form = document.getElementById('form');

const category = document.getElementById('category');

const imgInput = document.getElementById('imgInput');
const imgDispl = document.getElementById('imgDispl');

const submit = document.getElementById('submitButton');

imgInput.addEventListener('change', function (e) {
  if (imgInput.files && imgInput.files[0]) {
    var reader = new FileReader();
    reader.onload = function(x) {
      imgDispl.setAttribute('src', x.target.result);
      imgDispl.classList.add('d-block');
    };
    reader.readAsDataURL(imgInput.files[0]);
  }
});

submit.addEventListener('click', function (e) {
  
  if (category.value.trim().length == 0) {
    alert('Don\'t forget to add a category!');
    return;
  }
  else if (imgInput.files.length == 0) {
    alert('Don\'t forget to add an image!');
    return;
  }
  
  const XHR = new XMLHttpRequest();
  
  var FD = new FormData(form);
  
  XHR.addEventListener('load', function (e) {
    console.log('submitted!');
    counter += 1;
    docCount.innerHTML = counter.toString();
    imgInput.value = '';
    imgDispl.setAttribute('src', '');
    imgDispl.classList.remove('d-block');
  });
  
  XHR.addEventListener('error', function (e) {
    alert('something went wrong!');
    console.log('ahh!!');
  });
  
  XHR.open('POST', 'https://risleyarchives.com/submitPhoto')
  
  XHR.send(FD);
});
