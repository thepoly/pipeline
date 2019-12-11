from wagtail.core import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler
)

@hooks.register('register_rich_text_features')
def register_tooltip_feature(features):
    feature_name = 'tooltip'
    type_ = 'TOOLTIP'
    tag = 'div'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'TL',
        'description': 'Tooltip',
        'style': {
            'data-toggle':'tooltip',
            'data-placement': 'top',
            'title': "Some words"
        },
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {
            type_: {
                'element': tag,
                'props': {
                    #brokennnn
                }
            }
        }},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)