

export class CommentSlider {
    constructor(id) {
        this.commentTree = document.getElementById(id)
        this.nodeActivateHandler = null
    }

    onNodeActivate(callback) {
        this.nodeActivateHandler = callback
    }

    focusOnNode(comment) {
       this.clearCommentList()
       this.renderCommentList(comment)
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

    renderCommentList(comments) {
        self = this
        const tree = [comments]
        
        const ul = document.createElement("ul")
        ul.className = "comment-list"

        tree.forEach(comment => {
            ul.appendChild(this.renderComment(comment))
        });

        self.commentTree.appendChild(ul)
        self.commentTree.className = "open"
    }

    renderComment(comment) {
        const li = document.createElement("li")
        li.className = "comment"

        li.innerText = comment.author ?? comment.id


        if(comment.body !== undefined) {
            const container = document.createElement("div")
            const text = document.createElement("p")
            text.className = "comment-text"
            text.textContent = comment.body
            li.appendChild(container)
            container.appendChild(text)
        }
        

        if (comment.children.length > 0) {

            const toggleBtn = document.createElement("button")
            toggleBtn.className = "btn caret-btn"
            toggleBtn.innerHTML = `<i class="bi bi-caret-down"></i>`

            const childList = document.createElement("ul")
            childList.className = "comment-list"

            comment.children.forEach(child =>
                childList.appendChild(this.renderComment(child))
            )

            toggleBtn.onclick = () => {
                const collapsed = childList.classList.toggle("hidden")
                toggleBtn.innerHTML = collapsed
                    ? `<i class="bi bi-caret-right"></i>`
                    : `<i class="bi bi-caret-down"></i>`
            }

            li.insertBefore(toggleBtn, li.firstChild)
            li.appendChild(childList)
        }

        return li
    }


    render(comments) {
        self = this

        self.renderCommentList(comments)

        const closeButton = document.getElementById("comment-tree-close-button")
        closeButton.onclick = (event) => {self.commentTree.classList.remove("open")}
    }
}