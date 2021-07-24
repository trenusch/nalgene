import random
import numpy as np
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
                    pos = 0
                    while not child.raw_str[pos].isdigit():
                        pos += 1

                    weights.append(float(child.raw_str[pos: -1]))
                except Exception as e:
                    print("No activation found")
                    raise e
            weights = np.cumsum(weights)
            number = random.random() * weights[-1]
            i = 0
            while number > weights[i]:
                i += 1
            seq = current[i]
            # seq = random.sample(current, k=1)[0] , weights, k=1)[0]
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
            pos = 0
            while not child.raw_str[pos].isdigit():
                pos += 1
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
    children = [child.split(' ')[0] for child in parsed if child.split(' ')[0] != '%']
    to_remove = []
    for sentence in parsed['%']:
        sentence_split = sentence.raw_str.split(' ')
        sentence_split.remove('hat')    # quick fix for perfect
        for value in sentence_split:
            if value not in children:
                to_remove.append(sentence)
                break

    for sentence in to_remove:
        parsed['%'].remove_child(sentence)

    # remove sentences not using all given phrases
    if len(parsed['%']) == 0:
        return ""
    to_remove = {}
    for child in parsed:
        if not child.is_leaf and child.split(' ')[0] != '%':
            for sentence in parsed['%']:
                if child.split(' ')[0] not in sentence.raw_str:
                    if sentence in to_remove.keys():
                        to_remove[sentence] = to_remove[sentence] + 1
                    else:
                        to_remove[sentence] = 1
    if len(to_remove) != len(parsed['%']):
        for sentence in to_remove.keys():
            parsed['%'].remove_child(sentence)
    else:
        minimum = min(to_remove.values())
        for key in to_remove.keys():
            if to_remove[key] > minimum:
                parsed['%'].remove_child(key)

    parsed.map_leaves(tokenizeLeaf)

    walked_flat, walked_tree = walk_tree(parsed, parsed['%'], root_context['%'])
    #print(walked_flat)
    #print('>', fix_sentence(walked_flat.raw_str))
    #print(walked_tree)
    #print('-' * 80)
    return fix_sentence(walked_flat.raw_str)


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
