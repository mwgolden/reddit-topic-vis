

function onNodeMouseEnter(d3, event, data, links, domElement) {
    d3.select(domElement).raise()
        .select("circle")
        .transition()
        .attr("r", 5)


    // highlight all related links
    const related_links = new Set([
        ...data.ancestors(),
        ...data.descendants()
    ])

    links.classed("highlight", l =>
        related_links.has(l.source) &&
        related_links.has(l.target)
    )
}

function onNodeMouseLeave(d3, event, data, links, domElement) {
    d3.select(domElement)
        .select("circle")
        .transition()
        .attr("r", 1)

    links.classed("highlight", false)
}

function onNodeClick(d3, event, data, links, domElement) {
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