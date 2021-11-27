window.onload = function() {
    window.onhashchange = onHashChange;

    document.games = [];

    document.getElementById("search").oninput = filterSearch;
    randomBackground();

    fetch("games.json")
    .then((response) => response.json())
    .then((json) => {
        document.games = json;
        updateGames(json);
        onHashChange();
    })
}

function updateGames(games) {
    let gamesElem = document.getElementById("games");
    gamesElem.textContent = "";

    for (var i=0; i < games.length; i++) {
        let game = games[i];
        if (!game["href"].endsWith(".swf")) {
            continue;
        }
        
        let elem = document.importNode(document.getElementById("tpl-game").content, true);
        let link = elem.querySelectorAll("a")[0];
        link.setAttribute("href", "#" + game["id"]);
        link.textContent = game["name"];

        gamesElem.appendChild(elem);
    }
}

function filterSearch() {
    let q = document.getElementById("search").value;
    let g = [];

    if (q == "") {
        updateGames(document.games);
        return;
    }

    for (var i=0; i < document.games.length; i++) {
        let game = document.games[i];
        if (game.name.toLowerCase().includes(q.toLowerCase())) {
            g.push(game);
        }
    }

    updateGames(g)
}

function onHashChange() {
    let h = location.hash;
    console.log(h);
    if (!h.startsWith("#") || h == "#") {
        // Restore normal page

        let gz = document.getElementById("gamezone");
        gz.setAttribute("class", "hidden");
        document.getElementById("ruffle").textContent = "";

        let main = document.getElementById("searchzone");
        main.setAttribute("class", "");
        return;
    }
    // Show Game Zone
    let gz = document.getElementById("gamezone");
    gz.setAttribute("class", "");

    let main = document.getElementById("searchzone");
    main.setAttribute("class", "hidden");

    let gameId = h.substr(1);
    var game = undefined;
    for (var i=0; i < document.games.length; i++) {
        if (document.games[i].id == gameId) {
            game = document.games[i];
            break;
        }
    }

    if (game) {
        const ruffle = window.RufflePlayer.newest();
        const player = ruffle.create_player();
        const container = document.getElementById("ruffle");
        player.setAttribute("class", "ruffleplayer")
        container.textContent = "";
        container.appendChild(player);
        player.stream_swf_url(game.href);

        document.getElementById("description").getElementsByTagName("p")[0].textContent = game["description"];
        document.getElementById("gametitle").textContent = game["name"];
        document.getElementById("keys").textContent = "";

        for (const [key, text] of Object.entries(game["controls"])) {
            let li = document.createElement("li");
            if (key == "null") {
                li.innerHTML = text;
            }
            else if (["arrows", "mouse", "mouse-left", "mouse-right", "mouse-scroll"].includes(key)) {
                li.innerHTML = "<span class=\"" + key + "\"></span> " + text;
            }
            else {
                li.innerHTML = "<kbd>" + key + "</kbd> " + text;    
            }
            
            document.getElementById("keys").appendChild(li);
        }
    }
    else {
        alert("Bad link");
        document.location.href = "/";
    }
}