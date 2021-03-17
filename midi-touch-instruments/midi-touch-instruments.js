var instruments = (function() {

    var hexagon_coordinates = (center, radius, base_angle) => {
        return [0, 1, 2, 3, 4, 5].map(i => {
            let angle = i * Math.PI * 2 / 6 + base_angle;
            return {
                x: center.x + radius * Math.cos(angle),
                y: center.y + radius * Math.sin(angle)
            };
        })
    };

    var create_hexagon = (center, radius, base_angle, style) => {
        const hex = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        const spoints = hexagon_coordinates(center, radius, base_angle)
                        .map(p => p.x + " " + p.y + " ")
                        .reduce((s1, s2) => s1 + s2);
        hex.setAttribute("points", spoints);
        hex.setAttribute("style", style);
        return hex;
    };

    return {
        "hexagon_coordinates": hexagon_coordinates,
        "create_hexagon": create_hexagon
    };
})();