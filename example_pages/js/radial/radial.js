import { nodeEvents } from "./events.js"

export class Radial {
    constructor(id, d3) {
        this.d3 = d3
        this.chart = document.getElementById(id)
        this.chartWidth = Math.min(this.chart.clientWidth, this.chart.clientHeight)
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
        const svgRoot = d3.select(this.chart).select("svg")

        const cx = node.y * Math.cos(node.x - Math.PI/2)
        const cy = node.y * Math.sin(node.x - Math.PI/2)

        const width = +svgRoot.attr("width")
        const height = +svgRoot.attr("height")

        const scale = this.scale || 1

        const tx = width/2 - cx * scale
        const ty = height/2 - cy * scale

        const newTransform = d3.zoomIdentity
            .translate(tx, ty)
            .scale(scale)

        svgRoot.transition()
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

        const svgRoot = chart
            .append("svg")
                .attr("width", self.chartWidth)
                .attr("height", self.chartWidth)
                

        const svg = svgRoot
            .append("g")
                .attr("id", "radial-tree")

        self.zoom = d3.zoom()
            .scaleExtent([0.5, 5])
            .on("zoom", (event) => {
                self.scale = event.transform.k
                svg.attr("transform", event.transform)
            })

        // attach zoom to the SVG
        svgRoot.call(self.zoom)

        // set initial transform using same zoom instance
        svgRoot.call(
            self.zoom.transform,
            d3.zoomIdentity.translate(self.chartRadius, self.chartRadius).scale(1)
        )
        

        const hierarchy = d3.hierarchy(root)
        tree(hierarchy)

        // links
        svg.append("g")
                .attr("id", "radial-links")
            .selectAll("path")
            .data(hierarchy.links())
            .enter()
            .append("path")
            .attr("class", "link")
            .attr("d", d3.linkRadial()
                .angle(d => d.x)
                .radius(d => d.y))

        //nodes
        const node = svg.append("g")
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