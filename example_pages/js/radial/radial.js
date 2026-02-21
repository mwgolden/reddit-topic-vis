import { nodeEvents } from "./events.js"

export class Radial {
    constructor(id, d3) {
        this.d3 = d3
        this.chart = document.getElementById(id)
        this.chartWidth = Math.max(window.innerWidth, window.innerHeight) / 2
        this.chartRadius = this.chartWidth / 2
        this.clickHandler = null
        this.zoom = null  // only create one zoom per svg
        this.scale = 1
    }

    onNodeClick(callback) {
        this.clickHandler = callback
    }

    focusOnNode(node) {
    const d3 = this.d3
    const svg = d3.select(this.chart).select("svg")

    const cx = node.y * Math.cos(node.x - Math.PI/2)
    const cy = node.y * Math.sin(node.x - Math.PI/2)

    const scale = this.scale || 1

    const newTransform = d3.zoomIdentity
        .translate(
            this.chartRadius - cx * scale,
            this.chartRadius - cy * scale
        )
        .scale(scale)

    svg.transition()
        .duration(750)
        .call(this.zoom.transform, newTransform)
    }

    render(root) {

        const self = this
        const d3 = self.d3

        const tree = d3.tree()
            .size([2 * Math.PI, self.chartRadius - 60])

        const chart = d3.select(self.chart)

        // clear previous chart
        chart.selectAll("svg").remove()

        const svg = chart
            .append("svg")
                .attr("width", self.chartWidth)
                .attr("height", self.chartWidth)
                .attr("id", "radial-tree")
                

        const zoomContainer = svg.append("g")
                

        self.zoom = d3.zoom()
            .scaleExtent([0.5, 5])
            .on("zoom", (event) => {
                self.scale = event.transform.k
                zoomContainer.attr("transform", event.transform)
            })

        // attach zoom to the SVG
        svg.call(self.zoom)

        // set initial transform using same zoom instance
        svg.call(
            self.zoom.transform,
            d3.zoomIdentity.translate(self.chartRadius, self.chartRadius).scale(1)
        )
        

        const hierarchy = d3.hierarchy(root)
        tree(hierarchy)

        // links
        zoomContainer.append("g")
                .attr("id", "radial-links")
            .selectAll("path")
            .data(hierarchy.links())
            .enter()
            .append("path")
            .attr("vector-effect", "non-scaling-stroke")
            .attr("shape-rendering", "geometricPrecision")
            .attr("class", "link")
            .attr("d", d3.linkRadial()
                .angle(d => d.x)
                .radius(d => d.y))

        //nodes
        const node = zoomContainer.append("g")
                .attr("id", "radial-nodes")
            .selectAll("g")
            .data(hierarchy.descendants())
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", d => `rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y},0)`)
            .on(Object.keys(nodeEvents).join(" "), function(event, d){
                const handler = nodeEvents[event.type]
                handler(d3, event, d, this)

                if (event.type == "click" && self.clickHandler) {
                    self.clickHandler(event, d, this)
                }
            })
        
        node.append("circle").attr("r", 1)
        node.append("title")
            .text(d => `${d.data.author || ""}\n${d.data.comment || ""}`)       

    }
}