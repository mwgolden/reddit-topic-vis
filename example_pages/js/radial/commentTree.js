

export class CommentTree {
    constructor(id, wunderbaum) {
        this.wunderbaum = wunderbaum
        this.commentTree = document.getElementById(id)
        this.nodeActivateHandler = null
        this.tree = null
        this.fullComments = null
        this.ready = new Promise(resolve => this._resolveReady = resolve)
    }

    onNodeActivate(callback) {
        this.nodeActivateHandler = callback
    }

    async focusOnNode(key) {
        await this.ready
        console.log("focus on node")
        console.log(key)
        this.updateTree(this.fullComments)
        const subtree = this.tree.keyMap.get(key)
        const data = subtree.data._sourceData
        this.updateTree(data)

       console.log(`subtree: ${subtree}`)
    }

    d3ToWunderbaum(node) {  
        return {
            id: node.name,
            key: node.name,
            title: `${Object.hasOwn(node, "author") ? node.author : ""}: ${Object.hasOwn(node, "body") ? node.body : node.name}`,
            expanded: true,
            children: node.children ? node.children.map(child => this.d3ToWunderbaum(child)): [],
            _sourceData: node
        }
    }

    updateTree(comments) {
        const wbComments = this.d3ToWunderbaum(comments)
        if (this.tree) { this.tree.load([wbComments]) }
    }

    __setCommentTree(comments) {
        this.fullComments = comments
    }

    render(comments) {
        self = this
        const wbComments = this.d3ToWunderbaum(comments)
        this.fullComments = comments
        this.tree = new this.wunderbaum.Wunderbaum({
            element: this.commentTree,
            source: [wbComments],
            expandParents: true,
            icon: false,
            activate: function(e) {
                self.nodeActivateHandler(e)
            },
            init: function() {
                console.log("Comment tree is ready")
                self._resolveReady()
            }
        })
    }
}