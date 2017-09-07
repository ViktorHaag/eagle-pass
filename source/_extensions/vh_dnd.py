# -*- coding: utf-8 -*-

from six import iteritems
from docutils import nodes, utils

import sphinx
from sphinx.util.nodes import split_explicit_title


def make_mm_role(base_url, prefix, mmtype):
    def _make_url(base_url, name, mmtype):
        if mmtype == 'monster':
            return '{}-{}#{}'.format(base_url, name.casefold()[:1], name)
        elif mmtype == 'creature':
            return '{}{}'.format(base_url, name.casefold())
        
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        text = utils.unescape(text)
        has_explicit_title, title, part = split_explicit_title(text)
        full_url = _make_url(base_url, part, mmtype)
        if not has_explicit_title:
            if prefix is None:
                title = full_url
            else:
                title = prefix + part
        pnode = nodes.reference(title, title, internal=False, refuri=full_url)
        return [pnode], []

    return role


def make_phb_role(base_url, prefix):
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        text = utils.unescape(text)
        has_explicit_title, title, part = split_explicit_title(text)
        full_url = '{}#{}'.format(base_url, part.casefold())
        if not has_explicit_title:
            if prefix is None:
                title = full_url
            else:
                title = prefix + part
        pnode = nodes.reference(title, title, internal=False, refuri=full_url)
        return [pnode], []

    return role


def make_item_role(base_url, prefix):
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        text = utils.unescape(text)
        has_explicit_title, title, part = split_explicit_title(text)
        full_url = '{}{}'.format(base_url, part.casefold())
        if not has_explicit_title:
            if prefix is None:
                title = full_url
            else:
                title = prefix + part
        pnode = nodes.reference(title, title, internal=False, refuri=full_url)
        return [pnode], []

    return role


def setup_link_roles(app):
    app.add_role('dnd-class', make_phb_role('https://www.dndbeyond.com/compendium/rules/phb/classes', None))
    app.add_role('dnd-creature',
                 make_mm_role('https://www.dndbeyond.com/monsters/', None, mmtype='creature'))
    app.add_role('dnd-monster',
                 make_mm_role('https://www.dndbeyond.com/compendium/rules/mm/monsters', None, mmtype='monster'))
    app.add_role('dnd-npc',
                 make_mm_role('https://www.dndbeyond.com/monsters/', None, mmtype='creature'))
    app.add_role('dnd-spell', make_phb_role('https://www.dndbeyond.com/compendium/rules/phb/spells', None))
    app.add_role('dnd-item', make_item_role('https://www.dndbeyond.com/magic-items/', None))


def setup(app):
    app.connect('builder-inited', setup_link_roles)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
