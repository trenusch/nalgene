from parse import *
import os
import json


# Generate tokens up to $value level

def walk_tree(root, current, context, start_w=0):
    # print('\n[%d walk_tree]' % start_w, '"' + current.key + '"', 'context', context)

    try:
        # evaluate chance node for weights
        if current.key.endswith("!"):
            weights = []
            for child in current:
                try:
                    pos = len(child.raw_str) - child.raw_str.index('.') + 1
                    weights.append(float(child.raw_str[-pos: -1]))
                except Exception as e:
                    print("No activation found")
                    raise e
            seq = random.choices(current, weights, k=1)[0]
        else:
            seq = random.choice(current)
    except Exception as e:
        print('Exception walking from current', current, context)
        raise e

    flat = Node('>')
    tree = Node(current.key)

    # TODO: Remove?
    if seq.is_leaf:
        print('flat seq', seq)
        flat.add(seq)
        tree.add(seq)
        print('tree flat', tree)
        return flat, tree

    for child in seq:
        # print('[%d walk_tree child]' % start_w, child)
        child_key = child.key
        # Optionally skip optional tokens
        if child_key.endswith('?'):
            child_key = child_key[:-1]
            if random.random() < 0.5:
                continue
        if child_key.endswith('/'):
            pos = child_key.index('.') - 1
            child_key = child_key[:pos]

        # Expandable word, e.g. %phrase or ~synonym
        if child_key.startswith(('%', '~', '$', '@')):

            # Existing value, pass in context
            try:
                sub_context = context[child_key]
                if sub_context is not None: print('sub context', sub_context)

            except Exception:
                # print('[ERROR] Key', child_key, 'not in', context)
                sub_context = None

            try:
                sub_flat, sub_tree = walk_tree(root, sub_context or root[child_key], context, start_w)
            except Exception as e:
                print('[ERROR] Key', child_key, 'not in', context)
                print('Exception walking from current', current, child_key, context)
                raise e

            # Add words to flat tree
            flat.merge(sub_flat)

            # Adjust position based on number of tokens
            len_w = len(sub_flat)
            sub_tree.position = (start_w, start_w + len_w - 1, len_w)
            start_w += len_w

            # Add to (or merge with) tree
            if not child_key.startswith('~'):
                if root[child_key].passthrough:
                    tree.merge(sub_tree)
                else:
                    tree.add(sub_tree)
            else:
                if tree.type == 'value':
                    tree.merge(sub_flat)

        # Terminal node, e.g. a word
        else:
            has_value_parent, parent_line = current.has_parent('value')
            start_w += 1
            len_w = 1
            if has_value_parent:
                tree.type = 'value'
                tree.key = '.'.join(parent_line)
                tree.add(child_key)
            elif current.type == 'value':
                tree.add(child_key)
            flat.add(child_key)

    return flat, tree


def fix_sentence(sentence):
    return fix_capitalization(fix_punctuation(fix_newlines(fix_spacing(sentence))))


all_punctuation = ',.!?'
end_punctuation = '.!?'


def fix_capitalization(sentence):
    return ''.join(map(lambda s: s.capitalize(), re.split(r'([' + end_punctuation + ']\s*)', sentence)))


def fix_punctuation(sentence):
    fixed = re.sub(r'\s([' + all_punctuation + '])', r'\1', sentence).strip()
    if fixed[-1:] not in end_punctuation:
        fixed = fixed + '.'
    return fixed


def fix_newlines(sentence):
    return re.sub(r'\s*\\n\s*', '\n\n', sentence).strip()


def fix_spacing(sentence):
    return re.sub(r'\s+', ' ', sentence)


def generate_from_file(base_dir, filename, root_context=None):
    if root_context is None:
        root_context = Node('%')
    parsed = parse_file(base_dir, filename)

    # remove sentences using phrases not given
    for child in parsed:
        if child.is_leaf:
            to_remove = []
            for c in parsed['%']:
                if child.raw_str in c.raw_str:
                    to_remove.append(c)
            for c in to_remove:
                parsed['%'].remove_child(c)

    # remove sentences not using all given phrases
    for child in parsed:
        if not child.is_leaf and child.split(' ')[0] != '%':
            to_remove = []
            for c in parsed['%']:
                if child.split(' ')[0] not in c.raw_str:
                    to_remove.append(c)
            for c in to_remove:
                parsed['%'].remove_child(c)

    parsed.map_leaves(tokenizeLeaf)

    walked_flat, walked_tree = walk_tree(parsed, parsed['%'], root_context['%'])
    #print(walked_flat)
    print('>', fix_sentence(walked_flat.raw_str))
    print(walked_tree)
    print('-' * 80)
    return parsed, walked_flat, walked_tree


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py [grammar].nlg")
        sys.exit()
    root_context = None
    filename = os.path.realpath(sys.argv[1])
    base_dir = os.path.dirname(filename)
    filename = os.path.basename(filename)
    if len(sys.argv) > 2:
        root_context = Node(sys.argv[2])

    generate_from_file(base_dir, filename, root_context)
