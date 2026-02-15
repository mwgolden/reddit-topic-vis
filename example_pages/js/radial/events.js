

function onNodeMouseEnter(d3, event, data, domElement) {
    d3.select(domElement).raise()
        .select("circle")
        .transition()
        .attr("r", 5)
}

function onNodeMouseLeave(d3, event, data, domElement) {
    d3.select(domElement)
        .select("circle")
        .transition()
        .attr("r", 1)
}

function onNodeClick(d3, event, data, domElement) {
    //console.log(data)
}

function onBucketClick(d3, event, data, domElement) {
    d3.selectAll(".bucket").classed("active", false)
    d3.select(domElement).classed("active", true)
}

const nodeEvents = {
    "mouseenter": onNodeMouseEnter,
    "mouseleave": onNodeMouseLeave,
    "click": onNodeClick
}

const bucketEvents = { "click": onBucketClick }

export { nodeEvents, bucketEvents }