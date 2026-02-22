import { Radial } from "./radial/radial.js"
import { Buckets } from "./radial/buckets.js"
import { CommentSlider } from "./radial/commentSlider.js"
import { SkewedBucketStrategy } from "./radial/bucketStrategy.js"

export default class App {
    constructor(d3, comments) {
        this.d3 = d3
        this.comments = comments
    }

    run() {
        const radial = new Radial("chart", this.d3)
        const buckets = new Buckets("bucketList", this.d3)
        const commentTree = new CommentSlider("commentTree", this.comments.root)
        let currentBucketIndex = 0

        buckets.onBucketClick(bucket => {
            currentBucketIndex = bucket.index
            radial.render(bucket.root)
            commentTree.focusOnNode(bucketArray[currentBucketIndex].root)
        })
        
        commentTree.onNodeActivate(e => {
            //console.log("A node was activated")
            //console.log(e.node.data._sourceData)
            //radial.focusOnNode(e.node.data)
        })

        radial.onNodeClick( (event, node, d3Element) => {
            const rootNode = node.data.parent == null
            if(rootNode) {
                commentTree.focusOnNode(bucketArray[currentBucketIndex].root)
            } else {
                const comment = this.comments.getCommentById(node.data.id)
                commentTree.focusOnNode(comment)
            }
            radial.focusOnNode(node)
        })

        const bucketStrategy = new SkewedBucketStrategy(this.comments)

        const bucketArray = bucketStrategy.mapCommentsToBuckets()

        radial.render(bucketArray[currentBucketIndex].root)

        buckets.render(bucketArray)

        commentTree.render(bucketArray[currentBucketIndex].root)


        this.d3.select(".bucket").classed("active", true)
    }
}