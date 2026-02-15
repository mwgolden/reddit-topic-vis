import { nodeEvents } from "./events.js"

export class Radial {
    constructor(id, d3) {
        this.d3 = d3
        this.chart = document.getElementById(id)
        this.chartWidth = Math.min(this.chart.clientWidth, this.chart.clientHeight)
        this.chartRadius = this.chartWidth / 2
        this.clickHandler = null
        this.scale = 1
    }

    onNodeClick(callback) {
        this.clickHandler = callback
    }

    focusOnNode(node) {
        const d3 = this.d3
        const g = d3.select(this.chart).select("g#radial-tree")

        // convert polar to Cartesian
        const cx = node.y * Math.cos(node.x - Math.PI/2)
        const cy = node.y * Math.sin(node.x - Math.PI/2)

        // select current scale
        const scale = this.scale || 1

        const svg = d3.select(this.chart).select("svg")
        const width = +svg.attr("width")
        const height = +svg.attr("height")

        // compute translation to center node
        const translateX = width/2 - cx * scale
        const translateY = height/2 - cy * scale

        g.transition()
        .duration(750)
        .attr("transform", `translate(${translateX},${translateY}) scale(${scale})`)
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
                .attr("transform", `translate(${self.chartRadius}, ${self.chartRadius})`)

        const zoom = d3.zoom()
            .scaleExtent([0.5, 5])
            .on("zoom", (event) => {
                self.scale = event.transform.k
                svg.attr("transform", `translate(${event.transform.x + self.chartRadius}, ${event.transform.y + self.chartRadius}) scale(${event.transform.k})`)
            })

        // attach zoom to the SVG
        svgRoot.call(zoom)

        

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