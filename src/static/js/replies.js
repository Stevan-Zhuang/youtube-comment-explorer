function setReplies(data) {
    console.log(data);
    for (ch = 0; ch < data["items"].length; ch++) {
        var replies = document.getElementById("replies");
        var repliesRow = replies.insertRow();

        var channelCol = repliesRow.insertCell();

        var channel = data["items"][ch];
        var img = document.createElement("img");
        img.className = "profile";
        img.src = channel["image_url"]
        channelCol.appendChild(img);

        var commentsCol = repliesRow.insertCell();

        var username = document.createElement("p");
        username.className = "username";
        username.innerHTML += channel["channel_name"];
        commentsCol.appendChild(username);

        for (rp = 0; rp < channel["comments"].length; rp++) {
            var comment = document.createElement("p");
            comment.className = "comment";

            var reply = channel["comments"][rp];
            
            reply_data = reply["content"] + "\n";
            reply_data += "👍" + reply["likes"].toString();
            reply_data += " " + reply["time_ago"]

            comment.innerHTML += reply_data;
            commentsCol.appendChild(comment);
        }
    }
}