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

    var create_hex_button_grid = (corner_center, radius, nrows, ncolumns, corner_note) => {
        const buttons = [],
            height = Math.sqrt(3) * radius;
        for (let row = 0; row < nrows; row++) {
            for (let col = 0; col < ncolumns; col++) {
                const center = {
                    x: corner_center.x + col * 1.5 * radius,
                    y: corner_center.y + (row * height + (col % 2) * height / 2)
                },
                hex = create_hexagon(center, radius, 0, "fill:rgb(11, 99, 161);stroke:rgb(189, 183, 183);stroke-width:1");
                hex.setAttribute("class", "button");
                hex.setAttribute("data-note", corner_note - row * 7 + Math.floor(col / 2) - (col % 2) * 3);
                buttons.push(hex);
            }
        }
        return buttons;
    }

    return {
        "hexagon_coordinates": hexagon_coordinates,
        "create_hexagon": create_hexagon,
        "create_hex_button_grid": create_hex_button_grid
    };
})();