class CommentTree {
    constructor(data) {
        this.id = data.name
        this.key = data.name
        this.author = data.author || undefined
        this.body = data.body || undefined
        this.score = data.score
        this.children = data.children ? data.children.map(child => new CommentTree(child)): [],
        this._sourceData =  data
    }

    findById(id) {
        // Check current node
        if (this.id === id) {
            return this
        }

        // Search children
        for (const child of this.children) {
            const found = child.findById(id)
            if (found) return found
        }

        return null
    }
}

export default class Comments {
    constructor(comments) {
        this.root = new CommentTree(comments)
        this.index = new Map() // build a map for O(1) lookups
        this.buildIndex(this.root)

        console.log(this.root)
    }

    buildIndex(node) {
        this.index.set(node.id, node)

        for (const child of node.children) {
            this.buildIndex(child)
        }
    }

    getCommentById(id) {
        return this.index.get(id) || null
    }

}