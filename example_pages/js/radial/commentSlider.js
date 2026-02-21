

export class CommentSlider {
    constructor(id) {
        this.commentTree = document.getElementById(id)
        this.nodeActivateHandler = null
    }

    onNodeActivate(callback) {
        this.nodeActivateHandler = callback
    }

    focusOnNode(comment) {
       console.log("focus on node")
       this.clearCommentList()
       this.render(comment)
       this.commentTree.classList.add("open")
       
    }

    clearCommentList() {
        const childrenArray = Array.from(this.commentTree.children)
        const target = childrenArray.reduce((found, child) => {
            return found || (child.classList.contains('comment-list') ? child : null)
        }, null)
        if(target) {
            target.remove()
        }
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
        const tree = [comments]
        
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