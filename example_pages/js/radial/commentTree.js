

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
       //await this.ready
       //console.log("focus on node")
       console.log(key)
       this.commentTree.classList.add("open")
       //this.updateTree(this.fullComments)
       //const subtree = this.tree.keyMap.get(key)
       //const data = subtree.data._sourceData
       //this.updateTree(data)

       //onsole.log(`subtree: ${subtree}`)
    }

    parseCommentTree(node) {  
        return {
            id: node.name,
            key: node.name,
            author: `${Object.hasOwn(node, "author") ? node.author : node.name}`,
            body: `${Object.hasOwn(node, "body") ? node.body : ""}`,
            score: node.score == undefined ? "" :  node.score,
            expanded: true,
            children: node.children ? node.children.map(child => this.parseCommentTree(child)): [],
            _sourceData: node
        }
    }

    updateTree(comments) {
         const tree = [self.parseCommentTree(comments)]
        if (this.tree) { this.tree.load([wbComments]) }
    }

    __setCommentTree(comments) {
        this.fullComments = comments
    }

    renderComment(comment) {

    const li = document.createElement("li")
    li.className = "comment"

    const container = document.createElement("div")

    const author = document.createElement("p")
    author.textContent = comment.author

    const text = document.createElement("p")
    text.textContent = comment.body

    li.innerText = comment.author
    li.className = "comment-label"
    li.appendChild(container)
    container.appendChild(text)

    if (comment.children.length > 0) {

        const toggleBtn = document.createElement("button")
        toggleBtn.className = "btn btn-link text-body p-0 border-0 mb-2"
        toggleBtn.innerHTML = `<i class="bi bi-caret-down-fill me-1 opacity-50"></i>`

        const childList = document.createElement("ul")
        childList.className = "comment-list"

        comment.children.forEach(child =>
            childList.appendChild(this.renderComment(child))
        )

        toggleBtn.onclick = () => {
            const collapsed = childList.classList.toggle("d-none")
            toggleBtn.innerHTML = collapsed
                ? `<i class="bi bi-caret-right-fill me-1 opacity-50"></i>`
                : `<i class="bi bi-caret-down-fill me-1 opacity-50"></i>`
        }

        li.insertBefore(toggleBtn, li.firstChild)
        li.appendChild(childList)
    }

    return li
}


    render(comments) {
        self = this
        const tree = [self.parseCommentTree(comments)]
        //console.log(tree)
        
        const ul = document.createElement("ul")
        ul.className = "comment-list"

        tree.forEach(comment => {
            ul.appendChild(this.renderComment(comment))
        });

        const closeButton = document.createElement("button")
        closeButton.className = "btn btn-link"
        closeButton.id = "comment-tree-close-button"
        closeButton.innerText = "x"
        closeButton.onclick = (event) => {self.commentTree.classList.remove("open")}
        self.commentTree.appendChild(closeButton)

        self.commentTree.appendChild(ul)
    }
}