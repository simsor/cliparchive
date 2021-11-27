function randomBackground() {
    var backgrounds = ["bg-0", "bg-1", "bg-2", "bg-3", "bg-4", "bg-5", "bg-6", "bg-7", "bg-8", "bg-9"];

    var bg = backgrounds[Math.floor(Math.random() * backgrounds.length)];
    document.getElementsByTagName("body")[0].setAttribute("class", bg);
}