import Vue from 'vue';
import Element from 'element-ui';
import locale from 'element-ui/lib/locale/lang/en';
import LazyElSelect from '@/components/proxy/LazyElSelect';
import CharacterCountInput from '@/components/proxy/CharacterCountInput';
import CustomRequiredFormItem from '@/components/proxy/CustomRequiredFormItem';

export default () => {
  Vue.use(Element, { locale });
  Vue.component(LazyElSelect.name, LazyElSelect);
  Vue.component(CharacterCountInput.name, CharacterCountInput);
  Vue.component(CustomRequiredFormItem.name, CustomRequiredFormItem);
};
