var width = 1000,
    height = 800;

var force = d3.layout.force()
    .charge( function(d) { return -35 * Math.sqrt(d.count)} )
    .linkDistance(50)
    .gravity(0.15)
    .size([width - 250, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/graph", function(error, graph) {

    var main = svg.append("g")
        .attr("class", "graph");

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var link = main.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function(d) { return 2 * d.strength; });

    var node = main.selectAll(".node_circle")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node_circle")
        .attr("r", function(d) { return 0.5 * Math.sqrt(d.count); })
        .style("fill", function(d) { return d.color; } )
        .on("mouseover", function(d) { mouseover_node(d); })
        .on("mouseout", function(d) { mouseout_node(d) })
        //.on("dblclick", function(d){ window.location.href=('http://wolnelektury.pl/katalog/motyw/' + d.name + '/') })
        .call(force.drag);

    var label = main.selectAll(".node_label")
        .data(graph.nodes)
        .enter().append("text")
        .attr("class", "node_label")
        .attr("dx", function(d) { return 2 + 0.5 * Math.sqrt(d.count); })
        .attr("dy", ".4em")
        .attr("font-family", "Verdana")
        .attr("font-size", 10)
        .style("fill", "#000000")
        .text(function(d) { return d.display_en; });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        // node
        //   .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

        label.attr("x", function(d) { return d.x; })
            .attr("y", function(d) { return d.y; });
    });

    var mouseover_node = function(z){

        var neighbors = {};
        neighbors[z.index] = true;

        link.filter(function(d){
            if (d.source == z) {
                neighbors[d.target.index] = true
                return true
            } else if (d.target == z) {
                neighbors[d.source.index] = true
                return true
            } else {
                return false
            }
        })
            .style("stroke-opacity", 1);

        node.filter(function(d){ return neighbors[d.index] })
            .style("stroke-width", 3);

        label.filter(function(d){ return !neighbors[d.index] })
            .style("fill-opacity", 0.2);

        label.filter(function(d){ return neighbors[d.index] })
            .attr("font-size", 16)

    };

    var mouseout_node = function(z){
        link
            .style("stroke-opacity", 0.2);

        node
            .style("stroke-width", 1)

        label
            .attr("font-size", 10)
            .style("fill-opacity", 1)

    };
});