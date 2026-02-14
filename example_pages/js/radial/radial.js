import { nodeEvents } from "./events.js"

export class Radial {
    constructor(id, d3) {
        this.d3 = d3
        this.chart = document.getElementById(id)
        this.chartWidth = Math.min(this.chart.clientWidth, this.chart.clientHeight)
        this.chartRadius = this.chartWidth / 2
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
                .attr("transform", `translate(${self.chartRadius}, ${self.chartRadius})`)

        

        const hierarchy = d3.hierarchy(root)
        tree(hierarchy)

        // links
        svg.append("g")
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
            .selectAll("g")
            .data(hierarchy.descendants())
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", d => `rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y},0)`)
            .on(Object.keys(nodeEvents).join(" "), function(event, d){
                const handler = nodeEvents[event.type]
               handler(d3, event, d, this)
            })
        
        node.append("circle").attr("r", 1)
        node.append("title")
            .text(d => `${d.data.author || ""}\n${d.data.comment || ""}`)

    }
}