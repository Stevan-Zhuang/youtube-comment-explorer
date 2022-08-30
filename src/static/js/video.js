function setVideo(data) {
    var videoBox = document.getElementById("video");

    var thumbnail = document.createElement("img");
    thumbnail.className = "thumbnail";
    thumbnail.src = data["thumbnail"];
    videoBox.appendChild(thumbnail);
    
    var title = document.createElement("p");
    title.className = "title";
    title.innerHTML += data["name"];
    videoBox.appendChild(title);
}