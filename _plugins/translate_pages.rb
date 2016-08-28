
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
  end

  class TranslatedPage < Page
    include FastGettext::Translation
    
    attr_reader :language
  
    def initialize(page, language)
      @language = language
      super(page.site, page.base, page.dir, page.name)
      fill_data
    end
    
    def activate
      FastGettext.locale = language
    end
    
    def fill_data
      activate
      data["language"]= language
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
    
    def content
      activate
      super
    end
    
  end

  class PotLocalizationPlugin < Generator
    safe true
    
    attr_reader :site
    
    def text_domain
      "website"
    end
    
    def pot_file
      translations_folder + "/" + text_domain + ".pot"
    end
    
    def languages
      site.config["languages"] || []
    end

    def generate(site)
      @site = site
      setup_translations
      add_translated_sites
    end
    
    def setup_translations
      translations = TranslationLogger.new

      languages.each do |language|
        repos = [
          FastGettext::TranslationRepository.build(text_domain, :type=>:logger, :callback=>translations),
          FastGettext::TranslationRepository.build(text_domain, :path => translations_folder, :type => :po)
        ]
        FastGettext.add_text_domain(text_domain, :type=>:chain, :chain=>repos)
      end
      
      FastGettext.text_domain = text_domain
      
      Hooks.register(:site, :post_write) do |_site, payload|
        if _site == site
          save_translations translations.translations
        end
      end
    end
    
    # use the "translations_folder" tag from the _config.yml or default "_i18n"
    def translations_folder
      site.source + "/" + (site.config["translations_folder"] || "_i18n")
    end
    
    def add_translated_sites
      languages = site.config['languages']
      translated_pages = []
      site.pages.reject! do |page|
        to_translate = page.data["translate"]
        if to_translate
          languages.each do |language|
            translated_pages << TranslatedPage.new(page, language)
          end
        end
        to_translate
      end
      site.pages.concat(translated_pages)
    end
    
    def save_translations(translations)
      site.config["exclude"] ||= []
      unless site.config["exclude"].include? pot_file
        site.config["exclude"] << pot_file 
      end
      File.open(pot_file, 'w') do |file|
        file.write('msgid ""
msgstr ""
"Project-Id-Version: \n"
"POT-Creation-Date: \n"
"PO-Revision-Date: \n"
"Last-Translator: \n"
"Language-Team: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: de\n"
"X-Generator: PotLocalizationPlugin\n"')
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
      candidate = _(@key)

      if candidate == ""
        candidate = @key
      end
      candidate
    end
  end
end

Liquid::Template.register_tag('t', Jekyll::LocalizeTag)
Liquid::Template.register_tag('translate', Jekyll::LocalizeTag)