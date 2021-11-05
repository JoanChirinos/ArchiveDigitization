var counter = 0;
const docCount = document.getElementById('docCount');

const form = document.getElementById('form');

const imgInput = document.getElementById('imgInput');
const imgDispl = document.getElementById('imgDispl');

const submit = document.getElementById('submitButton');

imgInput.addEventListener('change', function (e) {
  if (imgInput.files && imgInput.files[0]) {
    var reader = new FileReader();
    reader.onload = function(x) {
      imgDispl.setAttribute('src', x.target.result);
      imgDispl.visibility = 'visible';
    };
    reader.readAsDataURL(imgInput.files[0]);
  }
});

submit.addEventListener('click', function (e) {
  const XHR = new XMLHttpRequest();
  
  var FD = new FormData(form);
  
  XHR.addEventListener('load', function (e) {
    console.log('submitted!');
    counter += 1;
    docCount.innerHTML = counter.toString();
    imgInput.value = '';
    imgDispl.setAttribute('src', '');
    imgDispl.visibility = 'hidden';
  });
  
  XHR.addEventListener('error', function (e) {
    alert('something went wrong!');
    console.log('ahh!!');
  });
  
  XHR.open('POST', 'https://risleyarchives.com/submitPhoto')
  
  XHR.send(FD);
});
