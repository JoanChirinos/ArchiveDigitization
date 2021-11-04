const camAccessButton = document.getElementById('camAccess');

const camStream = document.getElementById('camStream');

var imageCapture;

const cameraButton = document.getElementById('cameraButton');

const photo = document.getElementById('imageInput');

var form = document.getElementById('imageForm');

const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
//const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

const seventyvh = Math.floor(0.7 * vh);
//const nintetyvw = Math.floor(0.9 * vw);

cameraButton.addEventListener('click', function (e) {
  console.log('photo\'d!');
  imageCapture.takePhoto()
  .then(blob => createImageBitmap(blob))
  .then(imageBitmap => {
    const canvas = document.getElementById('photoCanvas');
    drawCanvas(canvas, imageBitmap);
    
    var data = canvas.toDataURL('image/png');
    photo.setAttribute('value', data);
    
    
//    sendData();
    
  })
});

function sendData() {
  const XHR = new XMLHttpRequest();
  const FD = new FormData(form);
  
  
  XHR.addEventListener('load', function (event) {
    alert('success!');
  })
  XHR.addEventListener('error', function (event) {
    alert('Something went wrong! Please email Joan');
  })
  
  XHR.open('POST', 'http://127.0.0.1:5000/submitPhoto');
  XHR.send(FD);
}

camAccessButton.addEventListener('click', async (e) => {
  let w = Math.floor(seventyvh * (720/1080))
  const stream = await navigator.mediaDevices.getUserMedia({
    video: {
      height: {ideal: seventyvh},
      width: {ideal: w},
      facingMode: 'environment'
    },
    audio: false
  });
  camStream.srcObject = stream;
  camAccessButton.remove();
  
  let track = stream.getVideoTracks()[0];
  imageCapture = new ImageCapture(track);
  
  document.getElementById('hiddenCol').removeAttribute('hidden');
});

function drawCanvas(canvas, img) {
  canvas.width = getComputedStyle(canvas).width.split('px')[0];
  canvas.height = getComputedStyle(canvas).height.split('px')[0];
  let ratio  = Math.min(canvas.width / img.width, canvas.height / img.height);
  let x = (canvas.width - img.width * ratio) / 2;
  let y = (canvas.height - img.height * ratio) / 2;
  canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height,
      x, y, img.width * ratio, img.height * ratio);
}