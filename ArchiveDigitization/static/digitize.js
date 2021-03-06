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
  
//  if (category.value.trim().length == 0) {
//    alert('Don\'t forget to add a category!');
//    return;
//  }
  if (imgInput.files.length == 0) {
    alert('Don\'t forget to add an image!');
    return;
  }
  
  var selectedL = $('.selectpicker').find('option:selected');
  var selected = [];
  for (opt of selectedL) {
    selected = selected.concat(opt.value);
  }
  console.log(selected);

  if (selected.length == 0) {
    alert('Don\'t forget to add some tags!');
    return;
  }
  
  
  const XHR = new XMLHttpRequest();
  
  var FD = new FormData(form);
  
  

  FD.append('selected', selected);
  
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
  
  XHR.open('POST', 'https://risleyarchives.com/submitPhoto');
  
  XHR.send(FD);
});

window.onload = function (e) {

  var clicked = false;

  const s = document.getElementsByClassName('bootstrap-select');
  var sel = null;

  do {
    sel = s[0];
  }
  while (sel == null);
  
  sel.addEventListener('click', function (e) {
    if (clicked) {
      return;
    }
    else {
      clicked = true;
    }
    
    const cbs = document.querySelectorAll('[role="combobox"]');
    var cb = cbs[cbs.length - 1];
    
    const newTag = document.getElementById('newTag');
    
    newTag.addEventListener('click', function (e) {
      const XHR = new XMLHttpRequest();
      
      var FD = new FormData(form);
      
      var selectedL = $('.selectpicker').find('option:selected');
      var selected = [];
      for (opt of selectedL) {
        selected = selected.concat(opt.value);
      }
      console.log(selected);
      
      var newTagName = cb.value.trim();
      if (newTagName == "") {
        return;
      }
      
      FD.append('selected', selected);
      
      FD.append('newTag', cb.value.trim());
      
      XHR.addEventListener('load', function (e) {
        $('.selectpicker').empty();
        var r = XHR.responseText;
//        console.log(r);
//        console.log(JSON.parse(r));
//        console.log(JSON.parse(r)['response'])
        
        var tags = JSON.parse(r)['response'];
        console.log(r);
        var selectedTags = [];
        for (tag of tags) {
          let tag_id = tag[0];
          let name = tag[1];
          let isSelected = tag[2];
          
          if (isSelected) {
            selectedTags.push(tag_id);
          }
          $('.selectpicker').append(`<option value="${tag_id}">${name}</option>`);
        }
        $('.selectpicker').selectpicker('val', selectedTags);
        $('.selectpicker').selectpicker('refresh');
        $('.selectpicker').selectpicker('refresh');
        $('.selectpicker').selectpicker('refresh');
      });
      
      XHR.addEventListener('error', function(e) {
        alert('ah!')
      });
      
//      XHR.open('POST', 'https://risleyarchives.com/addTag');
      XHR.open('POST', '/addTag');
      XHR.send(FD);
//      console.log(FD.get('selected'));
    });
  });
  
};

var updateTags = function (allTags) {
  const sp = $('.selectpicker');
  sp.find('').remove();
  var selected = [];
  for (var tag of allTags) {
    let tagID = tag[0];
    let tagName = tag[1];
    let isSelected = tag[2];
    
    sp.append(`<option value="${tagID}">${tagName}</option>`);
    if (isSelected) {
      selected = selected.concat(tagName);
    }
  }
  sp.selectpicker('val', selected);
  sp.selectpicker('refresh');
}




//newTag.addEventListener('click', function (e) {
//  const search = document.querySelectorAll('[type="search"]');
//  const XHR = new XMLHttpRequest();
//  
//  var FD = new FormData(form);
//  
//  
//  XHR.addEventListener('load', function (e) {
//    
//  });
//  XHR.addEventListener('error', function (e) {
//    alert('ahh!');
//  });
//  
////  XHR.open('POST', 'https://risleyarchives.com/addTag');
////  XHR.send(FD);
//  console.log(search);
//});