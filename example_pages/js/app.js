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
        
        buckets.onBucketClick(bucket => {
            radial.render(bucket.root)
        })
        
        commentTree.onNodeActivate(e => {
            //console.log("A node was activated")
            //console.log(e.node.data._sourceData)
            //radial.focusOnNode(e.node.data)
        })

        radial.onNodeClick( (event, node, d3Element) => {

            const comment = this.comments.getCommentById(node.data.id)
            console.log(node.data)
            commentTree.focusOnNode(comment)
            radial.focusOnNode(node)
        })

        const bucketStrategy = new SkewedBucketStrategy(this.comments)

        const bucketArray = bucketStrategy.mapCommentsToBuckets()

        radial.render(bucketArray[0].root)

        buckets.render(bucketArray)
        //console.log(bucketArray[0].root)

        commentTree.render(bucketArray[0].root)


        this.d3.select(".bucket").classed("active", true)
    }
}