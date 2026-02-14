class SkewedBucketStrategy {
    constructor(root) {
        this.root = root
        this.bucketPercentages = [0.01, 0.03, 0.07, 0.14, 0.25, 0.50] // percent of comments after ordering by score
    }

    bucketLabel(bucketIndex) {
        if (bucketIndex === 0) return `Top ${Math.ceil(this.bucketPercentages[bucketIndex] * 100)}%`
        if (bucketIndex === this.bucketPercentages.length - 1) return `Bottom ${Math.ceil(this.bucketPercentages[bucketIndex] * 100)}%`
        return `${Math.ceil(this.bucketPercentages[bucketIndex] * 100)}% - ${Math.ceil(this.bucketPercentages[bucketIndex + 1] * 100)}%`
    }

    mapCommentsToBuckets() {
        const firstLevelComments = this.root.children || []

        const sortedComments = [...firstLevelComments].sort(
            (a, b) => (b.score || 0) - (a.score || 0)
        )

        const numComments = sortedComments.length
        const buckets = []

        let cursor = 0
        for (let i = 0; i < this.bucketPercentages.length; i++) {
            let end
            // Last bucket takes the remainder to avoid rounding issues
            if (i === this.bucketPercentages.length - 1) {
                end = numComments
            } else {
                end = cursor + Math.round(numComments * this.bucketPercentages[i])
            }
            const bucketRoot = {
                name: this.root.name,
                children: []
            }
            bucketRoot.children = sortedComments.slice(cursor, end)
            
            buckets.push({
                index: i,
                label: this.bucketLabel(i),
                root: bucketRoot,
                count: bucketRoot.children.length,
                meta: { pct: this.bucketPercentages[i] }
            })
            cursor = end
        }
        return buckets
    }
}

export {
    SkewedBucketStrategy
}