from django import forms


class SelectOptionsWithAttrs(forms.widgets.SelectMultiple):
    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        option_dict = super(
            SelectOptionsWithAttrs, self).create_option(name,
                                                        value,
                                                        label,
                                                        selected,
                                                        index,
                                                        subindex,
                                                        attrs)
        option_dict['attrs']['selected'] = 'selected'

        return option_dict
