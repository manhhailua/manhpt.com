import React from 'react';
import clsx from 'clsx';
import {useBlogPost} from '@docusaurus/plugin-content-blog/client';
import TagsListInline from '@theme/TagsListInline';
import styles from './styles.module.css';

export default function BlogPostItemFooter({className}) {
  const {metadata, isBlogPostPage} = useBlogPost();
  const {tags} = metadata;
  
  if (!tags || tags.length === 0) {
    return null;
  }

  return (
    <footer className={clsx(styles.blogPostFooter, className)}>
      <TagsListInline tags={tags} />
    </footer>
  );
}
