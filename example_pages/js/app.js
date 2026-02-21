import { Radial } from "./radial/radial.js"
import { Buckets } from "./radial/buckets.js"
import { CommentTree } from "./radial/commentSlider.js"
import { SkewedBucketStrategy } from "./radial/bucketStrategy.js"

export default class App {
    constructor(d3, wunderbaum) {
        this.d3 = d3
        this.wunderbaum = wunderbaum
    }

    run(data) {
        const radial = new Radial("chart", this.d3)
        const buckets = new Buckets("bucketList", this.d3)
        const commentTree = new CommentTree("commentTree", this.wunderbaum)

        buckets.onBucketClick(bucket => {
            radial.render(bucket.root)
            commentTree._setCommentTree(bucket.root)
            commentTree.updateTree(bucket.root)
        })

        commentTree.onNodeActivate(e => {
            //console.log("A node was activated")
            //console.log(e.node.data._sourceData)
            //radial.focusOnNode(e.node.data)
        })

        radial.onNodeClick( (event, data, node) => {
            commentTree.focusOnNode(data.data.name)
            radial.focusOnNode(data)
        })

        const bucketStrategy = new SkewedBucketStrategy(data)

        const bucketArray = bucketStrategy.mapCommentsToBuckets()

        radial.render(bucketArray[0].root)

        buckets.render(bucketArray)
        //console.log(bucketArray[0].root)

        commentTree.render(bucketArray[0].root)


        this.d3.select(".bucket").classed("active", true)
    }
}