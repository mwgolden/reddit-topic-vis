

export class CommentTree {
    constructor(id, wunderbaum) {
        this.wunderbaum = wunderbaum
        this.commentTree = document.getElementById(id)
        this.nodeActivateHandler = null
        this.tree = null
    }

    onNodeActivate(callback) {
        this.nodeActivateHandler = callback
    }

    d3ToWunderbaum(node) {

        return {
            id: node.name,
            title: `${node.name}: ${Object.hasOwn(node, "body") ? node.body : ""}`,
            expanded: true,
            children: node.children ? node.children.map(child => this.d3ToWunderbaum(child)): []
        }
    }

    updateTree(comments) {
        if (this.tree) { this.tree.destroy() }
        this.render(comments)
    }

    render(comments) {
        console.log(comments)
        const wbComments = this.d3ToWunderbaum(comments)
        console.log(wbComments)
        console.log(this.commentTree)
        this.tree = new this.wunderbaum.Wunderbaum({
            element: this.commentTree,
            source: wbComments,
            expandParents: true,
            icon: false
        })

        //this.tree.on("nodeActivate", (event, node) => {
        //    if (this.nodeActivateHandler) {
        //        this.nodeActivateHandler(event, node)
        //    }
        //})
    }
}