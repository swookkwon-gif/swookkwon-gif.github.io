import { visit } from 'unist-util-visit';

export default function remarkKoreanBold() {
  return (tree: any) => {
    visit(tree, 'text', (node, index, parent) => {
      if (!parent || typeof node.value !== 'string') return;
      
      const regex = /\*\*(.*?)\*\*/g;
      const text = node.value;
      if (!regex.test(text)) return;
      
      const children: any[] = [];
      let lastIndex = 0;
      
      // Reset regex index
      regex.lastIndex = 0;
      let match;
      
      while ((match = regex.exec(text)) !== null) {
        if (match.index > lastIndex) {
          children.push({
            type: 'text',
            value: text.slice(lastIndex, match.index)
          });
        }
        
        children.push({
          type: 'strong',
          children: [{ type: 'text', value: match[1] }]
        });
        
        lastIndex = regex.lastIndex;
      }
      
      if (lastIndex < text.length) {
        children.push({
          type: 'text',
          value: text.slice(lastIndex)
        });
      }
      
      if (index !== undefined) {
        parent.children.splice(index, 1, ...children);
        return index + children.length;
      }
    });
  };
}
