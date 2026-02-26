import { bucketEvents } from "./events.js"

export class Buckets {
    constructor(id, d3) {
        this.d3 = d3
        this.bucketContainer = document.getElementById(id)
        this.clickHandler = null
    }

    onBucketClick(callback) {
        this.clickHandler = callback
    }

    render(buckets) {
        const self = this
        const d3 = self.d3
        const listGroup = self.d3.select(self.bucketContainer)
            .append("ul")
                .attr("class", "list-group")

        listGroup
            .selectAll(".list-group-item")
            .data(buckets, d => d.index)
            .join("li")
            .attr("class", "bucket list-group-item")
            .html(bucket => 
                    `
                    <div>${bucket.label}</div>
                        <div style="font-size: 12px; opacity:0.7">
                            ${bucket.count} threads
                        </div>
                    `
                )
            .on(Object.keys(bucketEvents).join(" "), function(event, d){
                const handler = bucketEvents[event.type]
                handler(d3, event, d, this)
                if (event.type === "click") {
                    self.clickHandler(d)
                }
            })

    }
}
