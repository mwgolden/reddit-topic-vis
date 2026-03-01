import { STOP_WORDS, PROFANITY_WORDS } from "./stopWords.js"

class CommentTree {
    constructor(data, parent = null) {
        this.parent = parent
        this.id = data.name
        this.key = data.name
        this.author = data.author ?? ""
        this.body = data.body ?? ""
        this.score = data.score
        this.children = data.children ? data.children.map(child => new CommentTree(child, data.name)): [],
        this._sourceData =  data
        this.tokens = this.tokenizeComment(data.body ?? "")
    }

    tokenizeComment(commentBody) {
        const stopWords = new Set([...STOP_WORDS, ...PROFANITY_WORDS]);
        const tokens = commentBody
        .toLowerCase()
        .replace(/(^|\s)'|'(\s|$)/g, " ")       // remove stray apostrophes
        .match(/\p{L}[\p{L}\p{N}']*/gu) || [];

        const filteredTokens = tokens.filter(t => !stopWords.has(t));
        return new Set(filteredTokens)
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
    }

    buildIndex(node) {
        this.index.set(node.id, node)

        for (const child of node.children) {
            this.buildIndex(child)
        }
    }

    getCommentById(id) {
        return this.index.get(id) ?? undefined
    }

}