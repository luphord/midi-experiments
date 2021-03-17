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
    return {
        "hexagon_coordinates": hexagon_coordinates
    };
})();