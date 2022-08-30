var numLoaded = 0;
function setAllReplies(data, numToLoadTotal, numToLoad) {
    setNextReplies(data, numToLoadTotal, numToLoad)

    var load = document.createElement("button");
    load.className = "load";
    load.onclick = function () {
        setNextReplies(data, numToLoadTotal, numToLoad);
    };
    load.innerHTML = "Load more";
    document.getElementById("load-more").appendChild(load);
}

function setNextReplies(data, numToLoadTotal, numToLoad) {
    var loadUpTo;
    if (numLoaded + numToLoad >= numToLoadTotal) {
        loadUpTo = numToLoadTotal;
        document.getElementById("load-more").style.display = "none";
    } else {
        loadUpTo = numLoaded + numToLoad;
    }
    for (var ch = numLoaded; ch < loadUpTo; ch++) {
        setReplies(data["items"][ch]);
    }
    numLoaded = loadUpTo;
}

function setReplies(channel) {
    var replies = document.getElementById("replies");

    var repliesRow = replies.insertRow();

    var channelCol = repliesRow.insertCell();

    var img = document.createElement("img");
    img.className = "profile";
    img.src = channel["image_url"];
    channelCol.appendChild(img);

    var commentsCol = repliesRow.insertCell();

    var username = document.createElement("p");
    username.className = "username";
    username.innerHTML += channel["channel_name"].bold();
    commentsCol.appendChild(username);

    for (rp = 0; rp < channel["comments"].length; rp++) {
        var comment = document.createElement("p");
        comment.className = "comment";

        var reply = channel["comments"][rp];
        comment.innerHTML += reply["content"];

        var commentData = document.createElement("p");
        commentData.className = "comment-data";
        commentData.innerHTML += reply["time_ago"];
        commentData.innerHTML += " 👍" + reply["likes"].toString();
        comment.appendChild(commentData);

        commentsCol.appendChild(comment);
    }
}