<template>
  <b-field :label="label" :type="state[id]" :message="message" :expanded="expanded">
    <b-input :type="type ? type : 'text'"
      :id="id" :name="id" :placeholder="placeholder" :icon="icon" :autofocus="autofocus"
      :required="required" :value="value" @input="emitInputValue" @focus="resetState"
      @blur="checkValue" v-validate="validators"
                         :data-vv-as="label ? label : placeholder"></b-input>
  </b-field>
</template>

<script>
export default {
  name: 'input-bound-input-field',
  props: {
    type: String,
    id: String,
    name: String,
    label: String,
    placeholder: String,
    state: Object,
    helpMessage: {
      type: String,
      default: ''
    },
    icon: String,
    autofocus: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    expanded: {
      type: Boolean,
      default: false
    },
    value: [Number, String],
    validators: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      message: this.helpMessage
    }
  },
  methods: {
    checkValue (ev) {
      this.$validator.validate(this.id)
      var hasErrors = this.errors.has(this.id)
      this.state[this.id] = hasErrors ? 'is-danger' : 'is-success'
      this.message = hasErrors ? this.errors.first(this.id) : this.helpMessage
    },
    emitInputValue (value) {
      this.$emit('input', value.trim())
    },
    resetState (ev) {
      this.state[this.id] = ''
      this.message = this.helpMessage
    }
  }
}
</script>
