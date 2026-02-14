root.count() // adds node.value to every node which is the number of descendants including self
            root.children.sort((a, b) => b.value - a.value) // sort first level by number of descendants
            const maxLevel1 = 10 // keep top N comments
            root.children = root.children.slice(0, maxLevel1) // trim the tree

            // 2nd level
            let nodesL2 = root.children.flatMap(node => node.children)
            nodesL2.sort((a, b) => b.value - a.value)
            const maxLevel2 = 10
            nodesL2 = nodesL2.slice(0, maxLevel2)
            root.children = nodesL2
            root.count()
            
            assignAngle(root, 0, 2 * Math.PI)

            //console.log(root)
            
            tree(root);


            const svg = d3.select("svg")
            .append("g")
            .attr("transform", `translate(${radius},${radius})`);


            // Color scale by depth
            const color = d3.scaleSequential()
            .domain([0, 8])
            .interpolator(d3.interpolateCool);


            // Node size based on score
            const scoreExtent = d3.extent(root.descendants(), d => d.data.score || 1);
            const sizeScale = d3.scaleSqrt().domain(scoreExtent).range([2, 10]);


            // Links
            //svg.append("g")
            //.selectAll("path")
            //.data(root.links())
            //.enter()
            //.append("path")
            //.attr("class", "link")
            //.attr("d", d3.linkRadial()
            //.angle(d => d.x)
           // .radius(d => d.y));
            
           // Draw Link
           svg.selectAll("path")
            .data(root.links())
            .enter()
            .append("path")
            .attr("d", d => {
                const start = radialPoint(d.source)
                const end = radialPoint(d.target)
                return `MS{start[0]},${start[1]} L${end[0]},${end[1]}`
            })

            // Nodes
            const node = svg.append("g")
            .selectAll("g")
            .data(root.descendants())
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", d => `
            rotate(${d.x * 180 / Math.PI - 90})
            translate(${d.y},0)
            `);


            node.append("circle")
            .attr("r", d => 0.8)
            .attr("fill", d => color(d.depth));
            });