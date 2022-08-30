function setReplies(data) {
    for (ch = 0; ch < data["items"].length; ch++) {
        var replies = document.getElementById("replies");
        var repliesRow = replies.insertRow();

        var channelCol = repliesRow.insertCell();

        var channel = data["items"][ch];
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
}