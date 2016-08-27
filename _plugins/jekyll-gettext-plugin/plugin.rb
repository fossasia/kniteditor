
require 'fast_gettext'
require 'get_pomo'

require 'pry'

class TranslationLogger
  def initialize
    @translations = []
  end
  
  def get_translations
    return @translations
  end
  
  def call(unfound)
    @translations.push(unfound)
  end
end

module Jekyll

  class Site
    
    alias :process_org :process
    attr_accessor   :dest
    def process
      if !self.config['baseurl']
        self.config['baseurl'] = ""
      end
      
      # variables
      config['baseurl_root'] = self.config['baseurl']
      baseurl_org = self.config['baseurl']
      languages = self.config['languages']
      dest_org = self.dest

      # loop
      self.config['lang'] = languages.first
      puts
      puts "Building site for default language: \"#{self.config['lang']}\" to: " + self.dest
      self.load_translations
      process_org
      self.save_missing_translations
      
      languages.drop(1).each do |lang|

        # build site for language lang
        self.dest = self.dest + "/" + lang
        self.config['baseurl'] = self.config['baseurl'] + "/" + lang
        self.config['lang'] = lang
        puts "Building site for language: \"#{self.config['lang']}\" to: " + self.dest
        self.load_translations
        process_org
        self.save_missing_translations

        # reset variables for next language
        self.dest = dest_org
        self.config['baseurl'] = baseurl_org
      end
      puts 'Build complete'
    end

    def load_translations
      @all_translations = TranslationLogger.new
      @missing_translations = TranslationLogger.new

      repos = [
        FastGettext::TranslationRepository.build(self.config['lang'], :type=>:logger, :callback=>@all_translations),
        FastGettext::TranslationRepository.build(self.config['lang'], :type=>:logger, :callback=>@missing_translations),
        FastGettext::TranslationRepository.build(self.config['lang'], :path => self.source + "/_i18n", :type => :po)
      ]
      FastGettext.add_text_domain(self.config['lang'], :type=>:chain, :chain=>repos)

      FastGettext.text_domain = self.config['lang']
      FastGettext.locale = self.config['lang']
    end

    def save_missing_translations
      filename = self.source + "/_i18n/" + self.config['lang'] + '/' + self.config['lang'] + '.po'
      content = File.open(filename, "r:UTF-8").read()
      existing_translations = GetPomo.unique_translations(GetPomo::PoFile.parse(content))
      
      # ignores any keys that already exist
      missing_translations_msgids = @missing_translations.get_translations.reject {|msgid| existing_translations.find {|trans| trans.msgid == msgid}}
      
      final_translations = existing_translations
      
      missing_translations_msgids.each do |new_msgid|
        new_trans = GetPomo::Translation.new
        new_trans.msgid = new_msgid
        new_trans.msgstr = ""
        final_translations.push(new_trans)
      end
      
      # uncomment this to remove translations that were not used
      not_used = final_translations.reject { |trans| @all_translations.get_translations.find {|msgid| trans.msgid == msgid}}
      final_translations = final_translations.reject {|trans1| not_used.find {|trans2| trans1.msgid == trans2.msgid}}
      
      final_translations.sort_by!(&:msgid)
      
      File.open(filename, 'w'){|f|f.print(GetPomo::PoFile.to_text(final_translations))}
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
