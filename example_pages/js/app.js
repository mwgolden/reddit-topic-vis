import { Radial } from "./radial/radial.js"
import { Buckets } from "./radial/buckets.js"
import { SkewedBucketStrategy } from "./radial/bucketStrategy.js"

export default class App {
    constructor(d3) {
        this.d3 = d3
    }

    run(data) {
        const radial = new Radial("chart", this.d3)

        const buckets = new Buckets("bucketList", this.d3)

        buckets.onBucketClick(bucket => {
            radial.render(bucket.root)
        })

        const bucketStrategy = new SkewedBucketStrategy(data)

        const bucketArray = bucketStrategy.mapCommentsToBuckets()

        radial.render(bucketArray[0].root)

        buckets.render(bucketArray)

        this.d3.select(".bucket").classed("active", true)
    }
}