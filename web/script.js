
/*
document.getElementById('imageInput').addEventListener('change', handleFileSelect);

  function handleFileSelect(event) {
    const files = event.target.files;

    // Lấy đối tượng container để hiển thị hình ảnh
    const imageContainer = document.getElementById('imageContainer');

    // Xóa tất cả các hình ảnh cũ trước khi hiển thị hình mới
    imageContainer.innerHTML = '';

    // Lặp qua từng file được chọn
    for (const file of files) {
      // Tạo một đối tượng FileReader để đọc file
      const reader = new FileReader();

      // Lắng nghe sự kiện khi file được đọc thành công
      reader.onload = function (e) {
        // Tạo một đối tượng hình ảnh để hiển thị
        const img = document.createElement('img');
        img.src = e.target.result;
        img.alt = file.name;
        img.classList.add('uploadedImage');

        // Hiển thị hình ảnh trong container
        imageContainer.appendChild(img);
      };

      // Đọc file dưới dạng URL
      reader.readAsDataURL(file);
    }
  }
*/

function predict() {
    var fileInput = document.getElementById('imageInput');
    var resultDiv = document.getElementById('result');

    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var formData = new FormData();
        formData.append('file', file);

        axios.post('http://127.0.0.1:5000/predict_image', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(function(response) {
            var prediction = response.data;
            resultDiv.innerHTML = `<p>Class: ${prediction.class}</p><p>Confidence: ${prediction.confidence.toFixed(4)}</p>`;
        })
        .catch(function(error) {
            console.error(error);
            resultDiv.innerHTML = `<p>Error predicting autism: ${error.message}</p>`;
        });
    } else {
        resultDiv.innerHTML = '<p>No image selected.</p>';
    }
}

/*
var canvas = document.querySelector("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector('#myVidPlayer');

//w-width,h-height
var w, h;
canvas.style.display = "none";

// Set up the interval for capturing and predicting
var predictionInterval;

window.navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
            
            //new
            w = video.videoWidth;
            h = video.videoHeight
            
            canvas.width = w;
            canvas.height = h;

            // Set up the interval to capture and predict every 1000 milliseconds (1 second)
            predictionInterval = setInterval(captureAndPredict, 1000);
        };
	})
    .catch(error => {
        alert('You have to enable the mike and the camera');
    });

function captureAndPredict() {
    // Capture the current frame from the video stream
    context.fillRect(0, 0, w, h);
    context.drawImage(video, 0, 0, w, h);
    canvas.style.display = "block";

    // Convert the captured frame to base64 data URL
    var file = canvas.toDataURL('image/jpeg');

    // Send the captured image to the server for prediction
    sendImageToServer(file);
}

function sendImageToServer(file) {
    /*var formData = new FormData();
    var resultDiv = document.getElementById('result');


    var formData = new FormData();
    formData.append('file', file);
    console.log(formData);

    axios.post('http://127.0.0.1:5000/predict_video', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(function(response) {
        var prediction = response.data;
        resultDiv.innerHTML = `<p>Class: ${prediction.class}</p><p>Confidence: ${prediction.confidence.toFixed(2)}</p>`;
    })
    .catch(function(error) {
        console.error(error);
        resultDiv.innerHTML = `<p>Error predicting autism: ${error.message}</p>`;
    });
}

*/
