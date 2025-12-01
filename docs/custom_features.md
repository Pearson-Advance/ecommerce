# Custom features for E-commerce service.

## Get the course image URL from LMS.

### Context:

By default, the basket page fetches the course information from Discovery, but sometimes when the course is not yet indexed, E-commerce fails to retrieve the course information from Discovery.

### Feature:

To avoid getting a blank course image, this feature allows retrieving the course information from the LMS,
based on a setting called: ENABLE_GET_COURSE_INFO_FROM_LMS, if present, the course information wil be fetched and cached
from the LMS course API.

### How to test:

- Set ENABLE_GET_COURSE_INFO_FROM_LMS in any of the E-commerce settings files.
- Go to a basket page, i.e. "E-commerce-URL>/basket/add/?sku=COURSE-SKU.
- Check that the course information displayed is correct, including the course image.

## Custom setting in the site configuration.

### Context:

We need to be able to add custom configurations per Site (to enable certain functionality per Site), but the Site Configuration model does not allow us to add additional or custom configurations.

### Feature:

This feature adds a new field to the Site Configuration model called: Custom Settings. Using this field, we can add any key/value pair that will later be used, for example, in E-commerce themes.

### How to test:

- Run migrations: python manage.py migrate core
- Go to the E-commerce admin site.
- Go to the Site Configuration module.
- Create a new entry and you will see a new field called: Custom Settings.

## Template tag to get site configuration settings.

### Context:

Currently, if we want to customise some HTML templates with custom parameters from the Site Configuration model, we have to add the Site Configuration context to the view and then use it within the templates.

### Feature:

This feature extends the template tag called "settings_value" to get Site Configuration values using this tag within HTML templates avoiding changing the E-commerce code base.

### How to test:

- In any of the E-commerce templates add: {% load core_extras %}
- And then: <p>{% settings_value 'lms_url_root' as setting %}{{ setting }}</p>
- Check that the correct value is rendered when visiting the page.

## Additional languages.

### Feature:

Currently, only two languages are enabled (EN and ES) and the aim of this feature is to add support for AR, DE, ES-LA FR-CA, IT, PT-BR, ZH-CHS.

### How to test:

- Go to a basket page, i.e. "E-commerce-URL>/basket/add/?sku=COURSE-SKU.
- Open the Devtools window (F12 or CTRL+SHIFT+c).
- Depending on the browser, check the cookies section and modify the cookie "openedx-language-preference" to the desired value.

### Note:

To enable a language integration with the LMS, this feature needs a custom feature in edx-platform: https://github.com/Pearson-Advance/edx-platform/pull/69
