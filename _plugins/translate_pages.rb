
require 'fast_gettext'
require 'get_pomo'
require 'pry'

class TranslationLogger

  def initialize
    @translations = []
  end
  
  def call(unfound)
    @translations.push(unfound)
  end
  
  def translations
      @translations.map do |msgid|
        translation = GetPomo::Translation.new
        translation.msgid = msgid
        translation.msgstr = ""
        translation
      end
  end
end

module Jekyll

  class Page
    attr_reader :base
    
    def activate
      raise "Add 'translate: true' to " + relative_path + "."
    end
  end
  
  class Site
    attr_accessor :pot_localization_plugin
  end

  class TranslatedPage < Page
    include FastGettext::Translation
    
    attr_reader :language, :default_language
  
    def initialize(page, language, default_language)
      @language = language
      @default_language = default_language
      super(page.site, page.base, page.dir, page.name)
      fill_data
    end
    
    def activate
      FastGettext.locale = language
    end
    
    def fill_data
      activate
      data["language"]= language
      data["default_language"]= default_language
      translate = data["translate"]
      if translate.is_a? Hash
        translate.each_pair do |key, value|
          data[key] = _(value)
        end
      end
    end
    
    def url
      "/" + language + super
    end
  end

  class PotLocalizationPlugin < Generator
    safe true
    
    attr_reader :site, :translations
    
    def text_domain
      unless site.config.include? "text_domain"
        site.config["text_domain"] = "website"
      end
      site.config["text_domain"]
    end
    
    def pot_file
      translations_folder + "/" + text_domain + ".pot"
    end
    
    def languages
      unless site.config.include? "languages"
        site.config["languages"] = ["en"]
      end
      site.config["languages"]
    end
    
    def po_file(language)
      translations_folder + "/" + language + "/" + text_domain + ".po"
    end

    def generate(site)
      @site = site
      site.pot_localization_plugin = self
      setup_translations
      add_translated_sites
    end
    
    def setup_translations
      @translations = TranslationLogger.new
      
      renew_translations

      Hooks.register(:site, :pre_render) do |_site, payload|
        renew_translations
      end
      
      Hooks.register(:site, :post_write) do |_site, payload|
        if _site == site and not translations.nil?
          save_translations translations.translations
        end
      end
    end
    
    def renew_translations
      languages.each do |language|
        repos = [
          FastGettext::TranslationRepository.build(text_domain, :type=>:logger, :callback=>translations),
          FastGettext::TranslationRepository.build(text_domain, :path => translations_folder, :type => :po)
        ]
        FastGettext.add_text_domain(text_domain, :type=>:chain, :chain=>repos)
      end
      FastGettext.text_domain = text_domain
   end

    
    # use the "translations_folder" tag from the _config.yml or default "_i18n"
    def translations_folder
      site.in_source_dir(site.config["translations_folder"] || "_i18n")
    end
    
    def add_translated_sites
      languages = site.config['languages']
      default_language = languages.first
      translated_pages = []
      site.pages.reject! do |page|
        to_translate = page.data["translate"]
        if to_translate
          languages.each do |language|
            translated_pages << TranslatedPage.new(page, language, default_language)
          end
        end
        to_translate
      end
      site.pages.concat(translated_pages)
    end
    
    def save_translations(translations)
      if translations.empty?
        return
      end
      site.config["exclude"] ||= []
      unless site.config["exclude"].include? pot_file
        site.config["exclude"] << pot_file 
      end
      File.open(pot_file, 'w') do |file|
        file.write('msgid ""
msgstr ""
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: ' + languages.first + '\n"
"X-Generator: ' + self.class.name + '\n"

')
        file.print(GetPomo::PoFile.to_text(translations))
      end
    end
  end

  class LocalizeTag < Liquid::Tag
    include FastGettext::Translation

    def initialize(tag_name, key, tokens)
      super
      @key = key.strip
    end

    def render(context)
      site = context.registers[:site]
      page = context.registers[:page]
      language = page["language"]
      if language.nil?
        default_language = page["default_language"].to_s
        raise ("Missing language! Either put 'language: " + default_language + 
               "' or 'translate: true' into the header")
      end
      add_localization_to_dependency(site, language, page["path"]) if page.key?("path")

      FastGettext.locale = language
      candidate = _(@key)

      if candidate == ""
        candidate = @key
      end
      candidate
    end
    
    def add_localization_to_dependency(site, language, path)
      po_file = site.pot_localization_plugin.po_file(language)
      puts ["add dependency", language, path, po_file].to_s
      site.regenerator.add_dependency(
        site.in_source_dir(path),
        po_file
      )
    end
  end
end

Liquid::Template.register_tag('t', Jekyll::LocalizeTag)
Liquid::Template.register_tag('translate', Jekyll::LocalizeTag)