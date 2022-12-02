# Custom types

The available content types within the Prismic model are located [here](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/prismic-model/src).


An example of a custom type for Articles: 

```
const articles: CustomType = {
  id: 'articles',
  label: 'Story',
  repeatable: true,
  status: true,
  json: {
    Story: {
      title,
      format: documentLink('Format', { linkedType: 'article-formats' }),
      body: articleBody,
    },
    Outro: {
      outroResearchItem: link('Outro: Research item'),
      outroResearchLinkText: singleLineText('Outro: Research link text', {
        overrideTextOptions: ['paragraph'],
      }),
      outroReadItem: link('Outro: Read item'),
      outroReadLinkText: singleLineText('Outro: Read link text', {
        overrideTextOptions: ['paragraph'],
      }),
      outroVisitItem: link('Outro: Visit item'),
      outroVisitLinkText: singleLineText('Outro: Visit link text', {
        overrideTextOptions: ['paragraph'],
      }),
    },
    Contributors: contributorsWithTitle(),
    Promo: {
      promo,
    },
    Metadata: {
      metadataDescription: singleLineText('Metadata description'),
    },
    'Content relationships': {
      series: list('Series', {
        series: documentLink('Series', { linkedType: 'series' }),
        positionInSeries: number('Position in series'),
      }),
      seasons: list('Seasons', {
        season: documentLink('Season', {
          linkedType: 'seasons',
          placeholder: 'Select a Season',
        }),
      }),
      parents: list('Parents', {
        order: number('Order'),
        parent: documentLink('Parent', {
          linkedType: 'exhibitions',
          placeholder: 'Select a parent',
        }),
      }),
    },
    Overrides: {
      publishDate: {
        config: {
          label:
            'Override publish date rendering. This will not affect ordering',
        },
        type: 'Timestamp',
      },
    },
  },
};
```

and this resolves in Prismic as the below: 

```
{
  "Story" : {
    "title" : {
      "type" : "StructuredText",
      "config" : {
        "label" : "Title",
        "single" : "heading1",
        "useAsTitle" : true
      }
    },
    "format" : {
      "type" : "Link",
      "config" : {
        "label" : "Format",
        "select" : "document",
        "customtypes" : [ "article-formats" ]
      }
    },
    "body" : {
      "fieldset" : "Body content",
      "type" : "Slices",
      "config" : {
        "labels" : {
          "editorialImage" : [ {
            "name" : "featured",
            "display" : "Featured"
          }, {
            "name" : "supporting",
            "display" : "Supporting"
          }, {
            "name" : "standalone",
            "display" : "Standalone"
          } ],
          "gifVideo" : [ {
            "name" : "supporting",
            "display" : "Supporting"
          } ],
          "iframe" : [ {
            "name" : "supporting",
            "display" : "Supporting"
          }, {
            "name" : "standalone",
            "display" : "Standalone"
          } ],
          "vimeoVideoEmbed" : [ {
            "name" : "featured",
            "display" : "Featured"
          }, {
            "name" : "supporting",
            "display" : "Supporting"
          }, {
            "name" : "standalone",
            "display" : "Standalone"
          } ],
          "youtubeVideoEmbed" : [ {
            "name" : "featured",
            "display" : "Featured"
          }, {
            "name" : "supporting",
            "display" : "Supporting"
          }, {
            "name" : "standalone",
            "display" : "Standalone"
          } ],
          "editorialImageGallery" : [ {
            "name" : "standalone",
            "display" : "Standalone"
          }, {
            "name" : "frames",
            "display" : "Frames"
          } ],
          "quoteV2" : [ {
            "name" : "pull",
            "display" : "Pull"
          }, {
            "name" : "review",
            "display" : "Review"
          } ]
        },
        "choices" : {
          "text" : {
            "type" : "Slice",
            "fieldset" : "Text",
            "non-repeat" : {
              "text" : {
                "type" : "StructuredText",
                "config" : {
                  "multi" : "heading2,heading3,paragraph,strong,em,hyperlink,list-item,embed",
                  "label" : "Text"
                }
              }
            }
          },
          "editorialImage" : {
            "type" : "Slice",
            "fieldset" : "Captioned image",
            "non-repeat" : {
              "image" : {
                "type" : "Image",
                "config" : {
                  "label" : "Image",
                  "thumbnails" : [ {
                    "name" : "32:15",
                    "width" : 3200,
                    "height" : 1500
                  }, {
                    "name" : "16:9",
                    "width" : 3200,
                    "height" : 1800
                  }, {
                    "name" : "square",
                    "width" : 3200,
                    "height" : 3200
                  } ]
                }
              },
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "paragraph,hyperlink,strong,em",
                  "label" : "Caption"
                }
              },
              "hasRoundedCorners" : {
                "type" : "Boolean",
                "config" : {
                  "default_value" : false,
                  "label" : "round image corners"
                }
              }
            }
          },
          "editorialImageGallery" : {
            "type" : "Slice",
            "fieldset" : "Image gallery",
            "non-repeat" : {
              "title" : {
                "type" : "StructuredText",
                "config" : {
                  "label" : "Title",
                  "single" : "heading1",
                  "useAsTitle" : true
                }
              }
            },
            "repeat" : {
              "image" : {
                "type" : "Image",
                "config" : {
                  "label" : "Image",
                  "thumbnails" : [ {
                    "name" : "32:15",
                    "width" : 3200,
                    "height" : 1500
                  }, {
                    "name" : "16:9",
                    "width" : 3200,
                    "height" : 1800
                  }, {
                    "name" : "square",
                    "width" : 3200,
                    "height" : 3200
                  } ]
                }
              },
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "paragraph,hyperlink,strong,em",
                  "label" : "Caption"
                }
              },
              "hasRoundedCorners" : {
                "type" : "Boolean",
                "config" : {
                  "default_value" : false,
                  "label" : "round image corners"
                }
              }
            }
          },
          "gifVideo" : {
            "type" : "Slice",
            "fieldset" : "Gif video",
            "non-repeat" : {
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "paragraph,hyperlink,strong,em",
                  "label" : "Caption"
                }
              },
              "tasl" : {
                "type" : "Text",
                "config" : {
                  "label" : "TASL",
                  "placeholder" : "title|author|sourceName|sourceLink|license|copyrightHolder|copyrightLink"
                }
              },
              "video" : {
                "type" : "Link",
                "config" : {
                  "label" : "Video",
                  "select" : "media",
                  "customtypes" : [ ],
                  "placeholder" : "Video"
                }
              },
              "playbackRate" : {
                "type" : "Select",
                "config" : {
                  "label" : "Playback rate",
                  "options" : [ "0.1", "0.25", "0.5", "0.75", "1", "1.25", "1.5", "1.75", "2" ]
                }
              },
              "autoPlay" : {
                "type" : "Boolean",
                "config" : {
                  "default_value" : true,
                  "label" : "Auto play"
                }
              },
              "loop" : {
                "type" : "Boolean",
                "config" : {
                  "default_value" : true,
                  "label" : "Loop video"
                }
              },
              "mute" : {
                "type" : "Boolean",
                "config" : {
                  "default_value" : true,
                  "label" : "Mute video"
                }
              },
              "showControls" : {
                "type" : "Boolean",
                "config" : {
                  "default_value" : false,
                  "label" : "Show controls"
                }
              }
            }
          },
          "iframe" : {
            "type" : "Slice",
            "fieldset" : "Iframe",
            "non-repeat" : {
              "iframeSrc" : {
                "type" : "Text",
                "config" : {
                  "label" : "iframe src",
                  "placeholder" : "iframe src"
                }
              },
              "previewImage" : {
                "type" : "Image",
                "config" : {
                  "label" : "Preview image"
                }
              }
            }
          },
          "standfirst" : {
            "type" : "Slice",
            "fieldset" : "Standfirst",
            "non-repeat" : {
              "text" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "strong,em,hyperlink",
                  "label" : "Standfirst"
                }
              }
            }
          },
          "quoteV2" : {
            "type" : "Slice",
            "fieldset" : "Quote",
            "non-repeat" : {
              "text" : {
                "type" : "StructuredText",
                "config" : {
                  "multi" : "paragraph,hyperlink,strong,em",
                  "label" : "Quote"
                }
              },
              "citation" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "paragraph,hyperlink,strong,em",
                  "label" : "Citation"
                }
              }
            }
          },
          "embed" : {
            "type" : "Slice",
            "fieldset" : "Embed",
            "non-repeat" : {
              "embed" : {
                "type" : "Embed",
                "fieldset" : "Embed"
              },
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "hyperlink,em",
                  "label" : "Caption",
                  "placeholder" : "Caption"
                }
              }
            }
          },
          "soundcloudEmbed" : {
            "type" : "Slice",
            "fieldset" : "SoundCloud embed",
            "non-repeat" : {
              "iframeSrc" : {
                "type" : "Text",
                "config" : {
                  "label" : "iframe src"
                }
              }
            }
          },
          "vimeoVideoEmbed" : {
            "type" : "Slice",
            "fieldset" : "Vimeo video",
            "non-repeat" : {
              "embed" : {
                "type" : "Embed",
                "fieldset" : "Vimeo embed"
              }
            }
          },
          "instagramEmbed" : {
            "type" : "Slice",
            "fieldset" : "Instagram embed",
            "non-repeat" : {
              "embed" : {
                "type" : "Embed",
                "fieldset" : "Instagram embed"
              }
            }
          },
          "twitterEmbed" : {
            "type" : "Slice",
            "fieldset" : "Twitter embed",
            "non-repeat" : {
              "embed" : {
                "type" : "Embed",
                "fieldset" : "Twitter embed"
              }
            }
          },
          "youtubeVideoEmbed" : {
            "type" : "Slice",
            "fieldset" : "[Deprecated] YouTube video (please use embed)",
            "non-repeat" : {
              "embed" : {
                "type" : "Embed",
                "fieldset" : "YouTube embed"
              },
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "hyperlink,em",
                  "label" : "Caption",
                  "placeholder" : "Caption"
                }
              }
            }
          },
          "discussion" : {
            "type" : "Slice",
            "fieldset" : "Discussion",
            "non-repeat" : {
              "title" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "heading2",
                  "label" : "Title"
                }
              },
              "text" : {
                "type" : "StructuredText",
                "config" : {
                  "multi" : "paragraph,hyperlink,strong,em",
                  "label" : "Text"
                }
              }
            }
          },
          "tagList" : {
            "type" : "Slice",
            "fieldset" : "Tag List",
            "non-repeat" : {
              "title" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "heading2",
                  "label" : "Title"
                }
              }
            },
            "repeat" : {
              "link" : {
                "type" : "Link",
                "config" : {
                  "label" : "Link",
                  "select" : "web",
                  "customtypes" : [ ]
                }
              },
              "linkText" : {
                "type" : "Text",
                "config" : {
                  "label" : "Link text"
                }
              }
            }
          },
          "imageList" : {
            "type" : "Slice",
            "fieldset" : "[Deprecated] Image list (please use captioned image or image gallery)",
            "non-repeat" : {
              "listStyle" : {
                "type" : "Select",
                "config" : {
                  "options" : [ "numeric" ],
                  "label" : "List style"
                }
              },
              "description" : {
                "type" : "StructuredText",
                "config" : {
                  "multi" : "paragraph,hyperlink,em",
                  "label" : "Description"
                }
              }
            },
            "repeat" : {
              "title" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "heading1",
                  "label" : "Title"
                }
              },
              "subtitle" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "heading2",
                  "label" : "Subtitle"
                }
              },
              "image" : {
                "type" : "Image",
                "config" : {
                  "label" : "Image"
                }
              },
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "strong,em,hyperlink",
                  "label" : "Caption"
                }
              },
              "description" : {
                "type" : "StructuredText",
                "config" : {
                  "multi" : "paragraph,hyperlink,em",
                  "label" : "Description"
                }
              }
            }
          },
          "audioPlayer" : {
            "type" : "Slice",
            "fieldset" : "Audio Player",
            "non-repeat" : {
              "title" : {
                "type" : "StructuredText",
                "config" : {
                  "label" : "Title",
                  "single" : "heading1",
                  "useAsTitle" : true
                }
              },
              "audio" : {
                "type" : "Link",
                "config" : {
                  "label" : "Audio",
                  "select" : "media",
                  "customtypes" : [ ]
                }
              }
            }
          }
        }
      }
    }
  },
  "Outro" : {
    "outroResearchItem" : {
      "type" : "Link",
      "config" : {
        "label" : "Outro: Research item",
        "customtypes" : [ ],
        "select" : null
      }
    },
    "outroResearchLinkText" : {
      "type" : "StructuredText",
      "config" : {
        "single" : "paragraph",
        "label" : "Outro: Research link text"
      }
    },
    "outroReadItem" : {
      "type" : "Link",
      "config" : {
        "label" : "Outro: Read item",
        "customtypes" : [ ],
        "select" : null
      }
    },
    "outroReadLinkText" : {
      "type" : "StructuredText",
      "config" : {
        "single" : "paragraph",
        "label" : "Outro: Read link text"
      }
    },
    "outroVisitItem" : {
      "type" : "Link",
      "config" : {
        "label" : "Outro: Visit item",
        "customtypes" : [ ],
        "select" : null
      }
    },
    "outroVisitLinkText" : {
      "type" : "StructuredText",
      "config" : {
        "single" : "paragraph",
        "label" : "Outro: Visit link text"
      }
    }
  },
  "Contributors" : {
    "contributors" : {
      "type" : "Group",
      "fieldset" : "Contributors",
      "config" : {
        "fields" : {
          "role" : {
            "type" : "Link",
            "config" : {
              "label" : "Role",
              "select" : "document",
              "customtypes" : [ "editorial-contributor-roles" ]
            }
          },
          "contributor" : {
            "type" : "Link",
            "config" : {
              "label" : "Contributor",
              "select" : "document",
              "customtypes" : [ "people", "organisations" ]
            }
          },
          "description" : {
            "type" : "StructuredText",
            "config" : {
              "multi" : "paragraph,hyperlink,strong,em",
              "label" : "Contributor description override"
            }
          }
        }
      }
    },
    "contributorsTitle" : {
      "type" : "StructuredText",
      "config" : {
        "single" : "heading1",
        "label" : "Contributors heading override"
      }
    }
  },
  "Promo" : {
    "promo" : {
      "type" : "Slices",
      "config" : {
        "label" : "Promo",
        "choices" : {
          "editorialImage" : {
            "type" : "Slice",
            "fieldset" : "Editorial image",
            "config" : {
              "label" : "Editorial image"
            },
            "non-repeat" : {
              "caption" : {
                "type" : "StructuredText",
                "config" : {
                  "single" : "paragraph",
                  "label" : "Promo text"
                }
              },
              "image" : {
                "type" : "Image",
                "config" : {
                  "label" : "Promo image",
                  "thumbnails" : [ {
                    "name" : "32:15",
                    "width" : 3200,
                    "height" : 1500
                  }, {
                    "name" : "16:9",
                    "width" : 3200,
                    "height" : 1800
                  }, {
                    "name" : "square",
                    "width" : 3200,
                    "height" : 3200
                  } ]
                }
              },
              "link" : {
                "type" : "Text",
                "config" : {
                  "label" : "Link override"
                }
              }
            }
          }
        }
      }
    }
  },
  "Metadata" : {
    "metadataDescription" : {
      "type" : "StructuredText",
      "config" : {
        "single" : "paragraph,hyperlink,strong,em",
        "label" : "Metadata description"
      }
    }
  },
  "Content relationships" : {
    "series" : {
      "type" : "Group",
      "fieldset" : "Series",
      "config" : {
        "fields" : {
          "series" : {
            "type" : "Link",
            "config" : {
              "label" : "Series",
              "select" : "document",
              "customtypes" : [ "series" ]
            }
          },
          "positionInSeries" : {
            "type" : "Number",
            "config" : {
              "label" : "Position in series"
            }
          }
        }
      }
    },
    "seasons" : {
      "type" : "Group",
      "fieldset" : "Seasons",
      "config" : {
        "fields" : {
          "season" : {
            "type" : "Link",
            "config" : {
              "label" : "Season",
              "select" : "document",
              "customtypes" : [ "seasons" ],
              "placeholder" : "Select a Season"
            }
          }
        }
      }
    },
    "parents" : {
      "type" : "Group",
      "fieldset" : "Parents",
      "config" : {
        "fields" : {
          "order" : {
            "type" : "Number",
            "config" : {
              "label" : "Order"
            }
          },
          "parent" : {
            "type" : "Link",
            "config" : {
              "label" : "Parent",
              "select" : "document",
              "customtypes" : [ "exhibitions" ],
              "placeholder" : "Select a parent"
            }
          }
        }
      }
    }
  },
  "Overrides" : {
    "publishDate" : {
      "config" : {
        "label" : "Override publish date rendering. This will not affect ordering"
      },
      "type" : "Timestamp"
    }
  }
}
```